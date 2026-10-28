import { createApp } from './app.ts';

const port = Number(process.env.PORT ?? 3000);
createApp().listen(port, () => console.log(`tasktrack api listening on :${port}`));
