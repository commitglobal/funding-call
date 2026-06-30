import { staffConst } from '@/types/User';
import { buildUrl } from '@/utils/buildUrl';


export const apiGetUrls = {
  dashboard: (isAdmin: boolean) =>
    buildUrl([staffConst, 'dashboard', isAdmin ? 'admin' : 'jury']),
};

export const apiPostUrls = {
};

export const apiDelUrls = {
};
