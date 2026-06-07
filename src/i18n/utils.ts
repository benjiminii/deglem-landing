import en from './en.json';
import mn from './mn.json';

export const languages = { en: 'English', mn: 'Монгол' } as const;
export type Lang = keyof typeof languages;
export const defaultLang: Lang = 'en';

const dictionaries: Record<Lang, Record<string, string>> = { en, mn };

export function useTranslations(lang: Lang) {
  const dict = dictionaries[lang] ?? dictionaries[defaultLang];
  return function t(key: string): string {
    return dict[key] ?? dictionaries[defaultLang][key] ?? key;
  };
}

/** Map a path between locales with consistent trailing slashes.
 *  '/' <-> '/mn/', '/privacy' -> '/privacy/' <-> '/mn/privacy/'. */
export function localizedPath(path: string, lang: Lang): string {
  let clean = path.replace(/^\/mn(\/|$)/, '/');
  if (!clean.endsWith('/')) clean += '/';
  if (lang === 'en') return clean;
  return clean === '/' ? '/mn/' : `/mn${clean}`;
}
