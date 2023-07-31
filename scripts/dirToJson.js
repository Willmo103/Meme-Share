const fs = require("fs");
const path = require("path");

// get the path where this script is located to know where to open the ignores.json file
const scriptPath = path.resolve(__dirname);
// parse the directory path from the command line
const dirPath = process.argv[2];
const savePathFlag = process.argv[3]
  ? process.argv[3] === "-s" || process.argv[3] === "--save"
  : false;
let saveToPath = "";
if (savePathFlag) {
  saveToPath = process.argv[4];
}
// parse the name of the starting dir from the path
const dirName = path.resolve(dirPath).split("\\").pop();

/**
 * dirToJson
 * @param {string} dirPath the path to the directory to be parsed
 * @param {string} saveToPath the path to save the json file to default: dirPath
 * @param {object} dirJson the object to save the file structure to for recursive calls. default: {}
 * file structure schema for dirJson:
 *
 * the function will recurse starting at the dirPath and build the
 * file structure moving forward only (no backtracking)
 */
const dirToJson = async (dirPath, dirJson = {}, _dirName = dirName) => {
  // check the directory path is valid
  await dirIsValid(dirPath);

  // create the dirName key in the dirJson object
  dirJson[_dirName] = {};

  // read the directory
  const dir = await readFiles(dirPath);

  // loop through the files in the directory
  for (let file of dir) {
    if (await isIgnoredFile(file)) {
      dirJson[_dirName][file] = { content: "ignored" };
    } else {
      // if the file is a directory recurse
      if (fs.lstatSync(`${dirPath}/${file}`).isDirectory()) {
        await dirToJson(`${dirPath}/${file}`, dirJson[_dirName], file);
      } else {
        // if the file is a file read the file and add the content to the dirJson object
        await fs.promises
          .readFile(`${dirPath}/${file}`, "utf8")
          .then((data) => {
            dirJson[_dirName][file] = data;
          })
          .catch((err) => {
            log(err);
            log(`unable to read ${file}`);
            dirJson[_dirName][file] = "Unreadable";
          });
      }
    }
  }
  return dirJson;
};

const getIgnoredFiles = async () => {
  // load the ignored files list from ignores.json
  const ignoredFiles = await fs.promises
    .readFile(`${scriptPath}/ignores.json`, "utf8")
    .then((data) => {
      return JSON.parse(data);
    })
    .catch((err) => {
      console.error(err);
      process.exit(1);
    });
  return ignoredFiles;
};

const addIgnored = async (file) => {
  // load the ignored files list from ignores.json
  const ignoredFiles = await getIgnoredFiles();

  // add the file to the list
  ignoredFiles.push(file);

  // write the list back to ignores.json
  await fs.promises
    .writeFile("./ignores.json", JSON.stringify({ ignoredFiles: ignoredFiles }))
    .then(() => log("ignores.json updated"))
    .catch((err) => {
      console.error(err);
      process.exit(1);
    });
};

const dirIsValid = async (dirPath) => {
  // check the directory path is valid
  await fs.promises
    .access(dirPath, fs.constants.F_OK)
    .then((res) => res)
    .catch((err) => {
      console.error(err);
      process.exit(1);
    });
};

const readFiles = async (dirPath) => {
  // read the directory
  const dir = await fs.promises
    .readdir(dirPath)
    .then((files) => {
      return files;
    })
    .catch((err) => {
      console.error(err);
      process.exit(1);
    });
  return dir;
};

const isIgnoredFile = async (file) => {
  let extension = "";

  // load the ignored files list from ignores.json
  const ignored = await getIgnoredFiles();
  const ignoredFiles = ignored.ignoredFiles;

  if (file.includes(".") && !file.startsWith(".")) {
    // get the extension to check if it is in the list
    extension = file.split(".").pop();
  }

  // check if the file is in the list
  if (extension === "") {
    return ignoredFiles.includes(file);
  } else {
    return ignoredFiles.includes(file) || ignoredFiles.includes(extension);
  }
};

const saveJson = async (saveToPath, dirJson) => {
  await fs.promises.writeFile(saveToPath, JSON.stringify(dirJson));
};

// Now call the main function
dirToJson(dirPath).then((dirJson) => {
  if (savePathFlag && saveToPath !== "") {
    try {
      saveJson(`${saveToPath}/${dirName}_directoryStructure.json`, dirJson);
    } catch (err) {
      console.error(err);
      process.exit(1);
    }
  } else {
    try {
      saveJson(`${dirPath}/${dirName}_directoryStructure.json`, dirJson);
    } catch (err) {
      console.error(err);
      process.exit(1);
    }
  }
});

const log = (message) => {
  try {
    fs.appendFileSync(`${scriptPath}/log.txt`, String(message));
  } catch {
    fs.writeFileSync(`${scriptPath}/log.txt`, String(message));
  }
}
