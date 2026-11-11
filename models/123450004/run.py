# Mata Kuliah: Deep Learning
# Nama: Luthfia Laila Ramadhani
# Komponen: Transfer Learning

"""Jalur TL (transfer learning) - Tim 18: status kipas, pompa, lampu dari urutan 4 frame.

Letakkan di models/<nim>/run.py. Jalankan dari akar repo:
    python models/<nim>/run.py --seed 1
    python models/<nim>/run.py --seed 1 --dummy     # uji kode saja, tanpa data.py

ASUMSI (cocokkan dengan Penjaga Data, lalu hapus tanda ini):
  - muat() -> X [N, 4, 3, 224, 224] (atau [N, 4, 224, 224, 3]) float32, sudah dinormalisasi
    dari data latih saja. y bilangan bulat 0..7 dengan sandi kelas = kipas*4 + pompa*2 + lampu.
  - Pemisahan val/test per blok cahaya ruang dilakukan di data.py, bukan di sini.
Model: ResNet18 pralatih (dibekukan) per frame -> fitur 4 frame digabung berurutan -> Linear(3).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torchvision

AKAR = Path(__file__).resolve().parents[2]
NIM = Path(__file__).resolve().parent.name
sys.path.insert(0, str(AKAR))


def ke_bit(y) -> np.ndarray:
    """Kelas 0..7 -> [N, 3] = (kipas, pompa, lampu)."""
    y = np.asarray(y).astype(np.int64).ravel()
    return np.stack([(y >> 2) & 1, (y >> 1) & 1, y & 1], axis=1).astype(np.float32)


def ke_kelas(bit: np.ndarray) -> np.ndarray:
    return (bit[:, 0] * 4 + bit[:, 1] * 2 + bit[:, 2]).astype(np.int64)


def siapkan(X) -> torch.Tensor:
    X = torch.as_tensor(np.asarray(X), dtype=torch.float32)
    if X.ndim != 5:
        raise SystemExit(f"X harus 5 dimensi [N, 4, C, H, W], dapat {tuple(X.shape)}")
    if X.shape[-1] == 3 and X.shape[2] != 3:  # [N, T, H, W, C] -> [N, T, C, H, W]
        X = X.permute(0, 1, 4, 2, 3).contiguous()
    return X


def buat_encoder() -> nn.Module:
    try:
        enc = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights.DEFAULT)
    except Exception as e:  # tanpa internet bobot tidak bisa diunduh
        print(f"PERINGATAN: bobot pralatih gagal dimuat ({e}); memakai bobot acak.")
        enc = torchvision.models.resnet18(weights=None)
    enc.fc = nn.Identity()
    for p in enc.parameters():
        p.requires_grad = False
    return enc.eval()


@torch.no_grad()
def ekstrak(enc: nn.Module, X: torch.Tensor, bs: int = 16) -> torch.Tensor:
    """[N, T, C, H, W] -> [N, T*512] (urutan frame dipertahankan agar putaran kipas terbaca)."""
    keluar = []
    for i in range(0, len(X), bs):
        xb = X[i:i + bs]
        n, t = xb.shape[:2]
        keluar.append(enc(xb.flatten(0, 1)).view(n, t * 512))
    return torch.cat(keluar)


def latih_kepala(F, B, epoch: int, seed: int) -> nn.Module:
    torch.manual_seed(seed)
    kepala = nn.Linear(F.shape[1], 3)
    opt = torch.optim.Adam(kepala.parameters(), lr=1e-3)
    loss_fn = nn.BCEWithLogitsLoss()
    B = torch.as_tensor(B)
    for _ in range(epoch):
        urut = torch.randperm(len(F))
        for i in range(0, len(F), 64):
            idx = urut[i:i + 64]
            opt.zero_grad()
            loss_fn(kepala(F[idx]), B[idx]).backward()
            opt.step()
    return kepala.eval()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--epoch", type=int, default=30)
    ap.add_argument("--dummy", action="store_true", help="data acak, hanya untuk menguji kode")
    a = ap.parse_args()

    np.random.seed(a.seed)
    torch.manual_seed(a.seed)

    if a.dummy:
        rng = np.random.default_rng(a.seed)
        Xtr, ytr = rng.normal(size=(48, 4, 3, 224, 224)).astype(np.float32), rng.integers(0, 8, 48)
        Xva, yva = rng.normal(size=(16, 4, 3, 224, 224)).astype(np.float32), rng.integers(0, 8, 16)
    else:
        from src.protokol import data
        Xtr, ytr, Xva, yva, _, _ = data.muat()  # data uji tidak disentuh (hanya sekali di sprint terakhir)

    t0 = time.time()
    Xtr, Xva = siapkan(Xtr), siapkan(Xva)
    enc = buat_encoder()
    Ftr, Fva = ekstrak(enc, Xtr), ekstrak(enc, Xva)
    kepala = latih_kepala(Ftr, ke_bit(ytr), a.epoch, a.seed)

    with torch.no_grad():
        bit_val = (torch.sigmoid(kepala(Fva)) > 0.5).numpy().astype(np.float32)
    pred = ke_kelas(bit_val)
    durasi = time.time() - t0

    # sanity check bentuk: 3 keluaran (kipas, pompa, lampu), kelas 0..7
    assert bit_val.shape == (len(Xva), 3) and pred.max() <= 7

    out = AKAR / "results" / NIM
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "pred_val.npy", pred)
    print(f"selesai: {len(pred)} prediksi val, {durasi:.1f} detik")

    if a.dummy:
        print("mode --dummy: evaluate dilewati (data.py belum diisi).")
        return
    subprocess.run([sys.executable, "-m", "src.common.evaluate", "--nim", NIM, "--model", "tl",
                    "--seed", str(a.seed), "--pred-val", str(out / "pred_val.npy"),
                    "--durasi", f"{durasi:.1f}", "--perangkat", "cpu laptop"],
                   cwd=AKAR, check=True)


if __name__ == "__main__":
    main()
