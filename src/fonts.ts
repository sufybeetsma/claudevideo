import {continueRender, delayRender, staticFile} from 'remotion';

const weights = [800, 900];
const handle = delayRender('Loading Montserrat');
Promise.all(
  weights.map((w) => {
    const face = new FontFace('Montserrat', `url(${staticFile(`fonts/montserrat-latin-${w}-normal.woff2`)}) format('woff2')`, {
      weight: String(w),
    });
    return face.load().then((f) => document.fonts.add(f));
  }),
)
  .then(() => continueRender(handle))
  .catch((err) => {
    console.error(err);
    continueRender(handle);
  });
