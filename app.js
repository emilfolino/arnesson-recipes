const tesseract = require("node-tesseract-ocr")

const config = {
  lang: "swe",
  oem: 1,
  psm: 3,
}

tesseract
  .recognize("recipe.jpeg", config)
  .then((text) => {
    console.log("Result:", text)
  })
  .catch((error) => {
    console.log(error.message)
  })
