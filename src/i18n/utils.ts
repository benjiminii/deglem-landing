import en from './en.json';
import mn from './mn.json';

export const languages = { mn: 'Монгол', en: 'English' } as const;
export type Lang = keyof typeof languages;
export const defaultLang: Lang = 'mn';

const dictionaries: Record<Lang, Record<string, string>> = { en, mn };

export function useTranslations(lang: Lang) {
  const dict = dictionaries[lang] ?? dictionaries[defaultLang];
  return function t(key: string): string {
    return dict[key] ?? dictionaries[defaultLang][key] ?? key;
  };
}

/** Map a path between locales with consistent trailing slashes.
 *  MN is the default (unprefixed) locale: '/' <-> '/en/', '/privacy' -> '/privacy/' <-> '/en/privacy/'. */
export function localizedPath(path: string, lang: Lang): string {
  let clean = path.replace(/^\/en(\/|$)/, '/');
  if (!clean.endsWith('/')) clean += '/';
  if (lang === defaultLang) return clean;
  return clean === '/' ? `/${lang}/` : `/${lang}${clean}`;
}
