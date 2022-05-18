const tesseract = require("node-tesseract-ocr")

const config = {
  lang: "swe",
  oem: 1,
  psm: 3,
}

tesseract
  .recognize("Resized_20220518_102015.jpeg", config)
  .then((text) => {
    console.log("Result:", text)
  })
  .catch((error) => {
    console.log(error.message)
  })
