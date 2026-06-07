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

/** Map a path between locales. '/' <-> '/mn/', '/privacy' <-> '/mn/privacy'. */
export function localizedPath(path: string, lang: Lang): string {
  const clean = path.replace(/^\/mn(\/|$)/, '/');
  if (lang === 'en') return clean;
  return clean === '/' ? '/mn/' : `/mn${clean}`;
}
