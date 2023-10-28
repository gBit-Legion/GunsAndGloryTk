from ultralytics import YOLO

model = YOLO('yolov8x.pt') 

results = model.train(data='config.yaml', 
                      epochs=300, 
                      batch=4, 
                      imgsz=1024, 
                      device=0, 
                      name="yolo8x_V0", 
                      optimizer='Adam', 
                      amp=False, 
                      dropout=0.3,
                      lr0=0.001,
                      lrf=1e-12,
                      augment=True,
                      save_period=1,
                      workers=1)