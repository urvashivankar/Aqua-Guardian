# 🎯 Dataset Collection - Quick Reference Card

## 4 Methods (Choose One)

### 1️⃣ KAGGLE (Easiest - 1 hour)
```
1. Visit: https://www.kaggle.com/search?q=water+pollution
2. Download dataset (requires free account)
3. Extract ZIP file
4. Run: python organize_dataset.py
```
**Best for:** Quick start, large datasets

---

### 2️⃣ GOOGLE IMAGES (Moderate - 3 hours)
```
1. pip install google_images_download Pillow
2. Download images (manual or automated)
3. Organize into folders:
   dataset_raw/
   ├── plastic/
   ├── sewage/
   ├── oil_spill/
   ├── foam/
   └── clean/
4. Run: python organize_dataset.py
```
**Best for:** Free, customizable

---

### 3️⃣ MANUAL (Best Quality - 1-2 weeks)
```
1. Take photos with smartphone
2. Visit local water bodies
3. Capture pollution types
4. Upload to dataset_raw/ folders
5. Run: python organize_dataset.py
```
**Best for:** Real-world, project-specific data

---

### 4️⃣ STOCK PHOTOS (Quick - 1 hour)
```
Sites:
- Unsplash.com (free)
- Pexels.com (free)
- Pixabay.com (free)

Download manually, organize, run script
```
**Best for:** Supplementing other sources

---

## What You Need

**5 Classes:**
- plastic (bottles, bags in water)
- sewage (discharge, contamination)
- oil_spill (oil slicks)
- foam (chemical foam)
- clean (pristine water)

**Quantity per class:**
- Minimum: 500 images
- Recommended: 1000 images
- Ideal: 2000+ images

**Quality:**
- Format: JPEG/PNG
- Size: 224x224 pixels minimum
- Good variety (angles, lighting)

---

## Quick Commands

```bash
# Create folder structure
mkdir -p dataset_raw/{plastic,sewage,oil_spill,foam,clean}

# Organize dataset
python backend/ml/organize_dataset.py

# Verify structure
ls backend/ml/dataset/train/

# Start training
python backend/ml/train_v2.py
```

---

## Fastest Path (2 Hours)

```
Hour 1: Download Kaggle dataset
        - Search "water pollution"
        - Download & extract
        - Rename folders to match our 5 classes

Hour 2: Organize & verify
        - Run organize_dataset.py
        - Check folder counts
        - Start training!
```

---

## Verification Checklist

Before training:
- [ ] train/ has 500+ images per class
- [ ] val/ has 100+ images per class
- [ ] test/ has 50+ images per class
- [ ] Images are >224x224 pixels
- [ ] No corrupted files
- [ ] Correctly labeled

---

## Search Terms for Google

**Plastic:**
"plastic bottles in river"
"plastic pollution water"
"plastic waste ocean"

**Sewage:**
"sewage discharge water"
"sewage pollution"
"wastewater contamination"

**Oil Spill:**
"oil spill water"
"oil slick ocean"
"petroleum pollution"

**Foam:**
"foam pollution river"
"chemical foam water"
"detergent pollution"

**Clean:**
"clear river water"
"clean lake pristine"
"unpolluted water"

---

## Expected Output

After running organize_dataset.py:

```
backend/ml/dataset/
├── train/
│   ├── plastic/      (700 images)
│   ├── sewage/       (700 images)
│   ├── oil_spill/    (700 images)
│   ├── foam/         (700 images)
│   └── clean/        (700 images)
├── val/
│   └── ... (200 each)
└── test/
    └── ... (100 each)

Total: 3,500 images
```

---

## Next Step

Once organized:
```bash
cd backend/ml
python train_v2.py
```

Wait 1-8 hours → Get trained model! 🎉

---

**Full Guide:** DATASET_COLLECTION_GUIDE.md
