const args = process.argv.slice(2);
const fs = require("fs");
const path = require("path");
const https = require("https");

const getMeme = async () => {
  const response = fetch("https://picsum.photos/1200/800")
    .then((response) => {
      if (verbose) {
        console.log("response:", response);
      }
      return response.url;
    })
    .catch((error) => {
      console.log("Error:", error);
    });
  return response;
};

// parse the args and set the variables
let savePath = process.cwd();
let numMemes = 3;
let verbose = false;
let help = false;
let arg;
for (let i = 0; i < args.length; i++) {
  arg = args[i];
  if (arg === "-p") {
    savePath = args[i + 1];
    i++;
  } else if (arg === "-v") {
    verbose = true;
  } else if (arg === "-h") {
    help = true;
  } else {
    numMemes = parseInt(arg);
  }
}

// if help is requested, print help and exit
if (help) {
  console.log(
    "Usage: node generate_memes.js [-p save_path] [num_memes] [-v] [-h]"
  );
  console.log("  -p: optional save path, default is current directory");
  console.log(
    "  num_memes: optional number of memes to generate, default is 3"
  );
  console.log("  -v: optional verbose");
  console.log("  -h: optional help");
  process.exit(0);
}

// if verbose, print the args
if (verbose) {
  console.log("savePath:", savePath);
  console.log("numMemes:", numMemes);
  console.log("verbose:", verbose);
}

// create the save path if it doesn't exist
if (!fs.existsSync(savePath)) {
  fs.mkdirSync(savePath);
}

// fetch the 'memes' from picsum.photos
for (let i = 0; i < numMemes; i++) {
  getMeme().then((url) => {
    if (verbose) {
      console.log("url:", url);
    }
    const fileName = path.join(savePath, `meme${i}.jpg`);
    const file = fs.createWriteStream(fileName);
    const request = https.get(url, (response) => {
      response.pipe(file);
    });
  });
}
