const fs = require("fs");
const path = require("path");
const chokidar = require("chokidar");

function createRefreshFile(targetDir) {
  const refreshFile = path.join(targetDir, "refresh.py");
  fs.writeFile(refreshFile, "", (err) => {
    if (err) {
      console.error(`Error creating refresh file: ${err.message}`);
    } else {
      console.log(`Refresh file created at: ${refreshFile}`);
      deleteRefreshFile(targetDir);
    }
  });
}

function deleteRefreshFile(targetDir) {
  const refreshFile = path.join(targetDir, "refresh.py");
  setTimeout(() => {
    fs.unlink(refreshFile, (err) => {
      if (err) {
        console.error(`Error deleting refresh file: ${err.message}`);
      } else {
        console.log(`Refresh file deleted: ${refreshFile}`);
      }
    });
  }, 2000); // Delay for 1 second to ensure that the file is created and detected by the file system.
}

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 2) {
    console.error("Usage: node watch_and_refresh.js <watch> <target>");
    process.exit(1);
  }

  const watchDir = args[0];
  const targetDir = args[1];

  if (!fs.existsSync(watchDir) || !fs.lstatSync(watchDir).isDirectory()) {
    console.error(`Error: '${watchDir}' is not a valid directory.`);
    process.exit(1);
  }

  if (!fs.existsSync(targetDir) || !fs.lstatSync(targetDir).isDirectory()) {
    console.error(`Error: '${targetDir}' is not a valid directory.`);
    process.exit(1);
  }

  const watcher = chokidar.watch(watchDir, {
    persistent: true,
    ignoreInitial: true,
  });

  watcher.on("all", (event, filePath) => {
    console.log(`File ${filePath} has been modified. Creating refresh file...`);
    createRefreshFile(targetDir);
  });

  console.log(
    `Watching directory '${watchDir}' for file changes. Press Ctrl+C to stop.`
  );
}

main();
