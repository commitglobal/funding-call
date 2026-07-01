import { SvgIcon } from '@/types/SvgIcon';
import { buildUrl } from '@/utils/buildUrl';

type UrlConfig = {
  component: string;
  name: string;
  icon?: SvgIcon;
};

export const urlsConfig: Record<string, UrlConfig> = {
  '/': { component: 'Public/Home/Index', name: 'Acasă' },
};

export const footerUrlsConfig: Record<string, UrlConfig> = {
  '/contact/': {
    component: 'Public/Contact/Index',
    name: 'Contact',
  },
};

const applicants = 'applicants';

export const applicantsUrls = {
  login: buildUrl([applicants, 'login']),
  register: buildUrl([applicants, 'register']),
};
