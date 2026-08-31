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

const auth = 'auth';

export const authUrls = {
  login: buildUrl([auth, 'login']),
  register: buildUrl([auth, 'register']),
};
