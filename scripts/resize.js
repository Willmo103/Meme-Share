const sharp = require('sharp');
const path = require('path');

const args = process.argv.slice(2);
const imagePath = args[0];
const size = args[1].split(':').map(Number);

sharp(imagePath)
    .resize(size[0], size[1])
    .toFile(path.join(path.dirname(imagePath), `resized_${path.basename(imagePath)}`), (err, info) => {
        if (err) throw err;
        console.log(info);
    });
