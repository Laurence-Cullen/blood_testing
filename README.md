# blood_testing
Ultra basic protype doing analysis of blood prick samples to diagnose anaemia automatically from images uploaded from mobile platforms.

Data path:
1. Image uploaded from phone
2. Image and student metadata uploaded to google cloud function 
3. Cloud function performs image analysis to determine the haemoglobin level in the sample
4. Haem levels and student data saved to firestore
