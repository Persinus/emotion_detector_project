const express = require('express')
const multer = require('multer')
const tf = require('@tensorflow/tfjs-node')
const fs = require('fs')
const path = require('path')

const app = express()
const port = 5000

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/')
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname)
  }
})
const upload = multer({ storage: storage })

// Tải mô hình deep learning
let model
async function loadModel() {
  model = await tf.loadLayersModel('file://path/to/your/model.json')
}
loadModel()

// Nhận diện cảm xúc
async function predictEmotion(imagePath) {
  const imageBuffer = fs.readFileSync(imagePath)
  const imageTensor = tf.node.decodeImage(imageBuffer)
  const inputTensor = imageTensor.expandDims(0).div(tf.scalar(255))
  const prediction = model.predict(inputTensor)

  const emotions = ['happy', 'sad', 'angry', 'surprised', 'disgust', 'fear', 'neutral']
  const result = prediction.dataSync()
  let resultObj = {}
  emotions.forEach((emotion, index) => {
    resultObj[emotion] = result[index]
  })

  return resultObj
}

// API nhận ảnh và trả về kết quả nhận diện
app.post('/api/predict', upload.single('image'), async (req, res) => {
  const imagePath = path.join(__dirname, 'uploads', req.file.filename)

  try {
    const prediction = await predictEmotion(imagePath)
    res.json(prediction)
  } catch (error) {
    res.status(500).send('Lỗi khi nhận diện cảm xúc')
  } finally {
    fs.unlinkSync(imagePath) // Xóa ảnh sau khi xử lý
  }
})

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`)
})
