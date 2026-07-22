const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

admin.initializeApp({ projectId: 'gept-org-br' });
const bucket = admin.storage().bucket('gept-org-br.appspot.com');

async function uploadFiles() {
  const audioDir = path.join(__dirname, '../app/public/audio');
  const files = fs.readdirSync(audioDir).filter(f => f.endsWith('.mp3'));
  const urls = {};

  for (const file of files) {
    console.log(`Uploading ${file}...`);
    const destination = `audio/${file}`;
    const token = uuidv4();
    
    await bucket.upload(path.join(audioDir, file), {
      destination: destination,
      metadata: {
        contentType: 'audio/mpeg',
        metadata: { firebaseStorageDownloadTokens: token }
      }
    });

    const url = `https://firebasestorage.googleapis.com/v0/b/${bucket.name}/o/${encodeURIComponent(destination)}?alt=media&token=${token}`;
    urls[file] = url;
    console.log(`Uploaded! URL: ${url}`);
  }
  
  fs.writeFileSync('uploaded_urls.json', JSON.stringify(urls, null, 2));
  console.log('Saved URLs to uploaded_urls.json');
}

uploadFiles().catch(console.error);
