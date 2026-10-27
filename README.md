# Mini Link Studio

A mobile-friendly photo editor and print-preparation companion for the original Fujifilm instax mini Link.

## Live app
https://mnemos-memory-coach.heyboernathan.workers.dev/

## Features
- Import a photo from your phone or computer
- Prepare portrait Instax Mini, landscape, square, or three-frame strip layouts
- Add captions and choose caption placement
- Apply original, warm film, black-and-white, soft-vintage, and bright filters
- Choose classic white, blush, midnight, or no border
- Add a QR code containing a hidden message or pointing to a video/webpage
- Export a PNG or share the print image to the official instax mini Link app

## Printing with the original mini Link
1. Open the live app on your phone.
2. Choose your photo and customize the print.
3. Tap **Save print image** or **Share image**.
4. Open the saved image in the official **instax mini Link** app.
5. Connect your printer over Bluetooth in the official app and print.

A normal mobile website cannot directly control the mini Link Bluetooth connection or reproduce every model-specific feature in Fujifilm's newer apps. This app prepares creative print images; the official app remains responsible for sending them to the printer.

## Local / alternate hosting
The production application is a Cloudflare Worker (worker.js). app.py and templates/index.html remain as a lightweight redirect for legacy Python hosting so they do not show the retired memory-training experience.
