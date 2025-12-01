# 🤖 Automated Dataset Download - Quick Guide

## ⚡ ONE-CLICK SOLUTION

**Just double-click this file:**
```
complete_ai_pipeline.bat
```

**That's it!** It will:
1. ✅ Download 1000+ images automatically (15-30 min)
2. ✅ Organize into train/val/test (2-5 min)
3. ✅ Train AI model (1-8 hours)
4. ✅ Save trained model to `backend/ml/model.pth`

**Total time:** 1-8 hours (mostly unattended)

---

## 📋 Or Run Step-by-Step

### Step 1: Download Images (15-30 min)
Double-click: `download_dataset.bat`

Or manually:
```powershell
pip install bing-image-downloader
cd backend\ml
python download_dataset.py
```

**What it downloads:**
- Plastic pollution: ~1200 images
- Sewage pollution: ~1200 images
- Oil spills: ~1200 images
- Foam pollution: ~1200 images
- Clean water: ~1200 images

**Total:** ~6000 images

---

### Step 2: Organize Dataset (2-5 min)
Double-click: `organize_dataset.bat`

Or manually:
```powershell
pip install Pillow
cd backend\ml
python organize_dataset.py
```

**Output:**
```
backend/ml/dataset/
├── train/ (70% - ~4200 images)
├── val/   (20% - ~1200 images)
└── test/  (10% - ~600 images)
```

---

### Step 3: Train Model (1-8 hours)
Double-click: `start_training.bat`

Or manually:
```powershell
pip install torch torchvision matplotlib seaborn scikit-learn
cd backend\ml
python train_v2.py
```

**What happens:**
- 50 epochs of training
- Progress shown in real-time
- Best model auto-saved
- Creates training curves
- Generates confusion matrix

**Output files:**
- `model.pth` - Trained model (ready to use!)
- `training_curves.png` - Accuracy/loss graphs
- `confusion_matrix.png` - Performance breakdown
- `classification_report.txt` - Detailed metrics

---

## ⏱️ Expected Timeline

| Step | Time | Can Leave? |
|------|------|------------|
| Download | 15-30 min | ❌ Monitor for errors |
| Organize | 2-5 min | ✅ Fully automatic |
| Training | 1-8 hours | ✅ Can minimize window |

**Total:** ~2-9 hours (mostly unattended)

---

## 💻 System Requirements

**Minimum:**
- Windows 10/11
- Python 3.9+
- 4GB RAM
- 10GB free disk space
- Internet connection

**Recommended:**
- 8GB+ RAM
- GPU (NVIDIA with CUDA) - 10x faster training
- 20GB+ free space

---

## 🆘 Troubleshooting

### Download fails
```powershell
# Try installing again
pip uninstall bing-image-downloader
pip install bing-image-downloader

# Or reduce image count
# Edit download_dataset.py, change:
IMAGES_PER_QUERY = 100  # Instead of 200
```

### "Module not found" error
```powershell
# Install all dependencies
pip install bing-image-downloader Pillow torch torchvision matplotlib seaborn scikit-learn
```

### Training is too slow
- Close other applications
- Use smaller batch size (edit train_v2.py: `BATCH_SIZE = 16`)
- Reduce epochs (edit train_v2.py: `EPOCHS = 20`)

### Out of memory during training
```python
# Edit train_v2.py, reduce batch size:
BATCH_SIZE = 16  # or even 8
```

---

## ✅ Verification

After completion, check:

1. **Model file exists:**
   ```
   backend/ml/model.pth (~150 MB)
   ```

2. **Accuracy is good:**
   - Open `training_curves.png`
   - Validation accuracy should be >85%

3. **Test inference:**
   ```powershell
   cd backend
   python -c "from ml.infer import predict_image; print('✅ Model loaded!')"
   ```

---

## 🎯 What's Next After Training?

Once `model.pth` is created:

1. ✅ **Phase 1 Complete!** (AI Training)
2. **Start Phase 2:** Blockchain deployment
3. **Read:** `implementation_plan.md` - Phase 2 section
4. **Or jump to:** Backend testing and deployment

---

## 🚀 RECOMMENDED: Just Run This!

**For the easiest experience:**

1. Double-click: **`complete_ai_pipeline.bat`**
2. Press `Y` when asked
3. Let it run for 2-9 hours
4. Come back to a trained model!

**That's all you need to do!** ✨

---

## 📊 Expected Results

After successful run:

```
✅ Downloaded: ~6000 images
✅ Organized: train/val/test splits
✅ Trained: 50 epochs
✅ Accuracy: >85% (target)
✅ Model: backend/ml/model.pth
✅ Ready: For Phase 2!
```

---

**Time to start:** Just double-click `complete_ai_pipeline.bat`! 🚀
