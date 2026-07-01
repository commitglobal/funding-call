import { staffConst } from '@/types/User';
import { buildUrl } from '@/utils/buildUrl';


export const apiGetUrls = {
  dashboard: (isAdmin: boolean) =>
    buildUrl([staffConst, 'dashboard', isAdmin ? 'admin' : 'jury']),
  usersSettings: buildUrl(['settings']),
};

export const apiPostUrls = {
  usersLogout: () => buildUrl(['logout']),
};

export const apiDelUrls = {
};
