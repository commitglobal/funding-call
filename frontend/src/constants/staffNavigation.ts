import { NavigationItem } from '@/types/NavigationItem';
import {
  DashboardIcon,
} from '@/components/dashboard-icons';
import { LightBulbIcon } from '@/components/LightBulbIcon';
import { apiGetUrls } from './apiUrls';

export const navigation: NavigationItem[] = [
  {
    name: 'Dashboard',
    href: apiGetUrls.dashboard(true),
    icon: DashboardIcon,
    userTypes: ['admin_basic', 'admin_super'],
  },
  {
    name: 'Dashboard',
    href: apiGetUrls.dashboard(false),
    icon: DashboardIcon,
    userTypes: ['judge'],
  },
  {
    name: 'Funding Call',
    icon: LightBulbIcon,
    items: [
    ],
    userTypes: ['admin_basic', 'admin_super'],
  },
];
