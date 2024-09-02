import {EditorView, basicSetup} from 'codemirror'
// import {javascript} from '@codemirror/lang-javascript'

export async function newEditor(lang, parent) {
  const extensions = [basicSetup]
  if (lang === 'javascript') {
    const javascript = await import('@codemirror/lang-javascript');
    extensions.push(javascript());
  } else if (lang !== '') {
    console.error(`Unsupported language: ${lang}`);
  }
  return new EditorView({extensions, parent});
}
