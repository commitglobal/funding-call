import { User, UserType } from '@/types/User';

export function isSuperAdmin(user: User) {
  return user.is_superadmin_member;
}

export function isAdmin(user: User) {
  return user.is_admin_member;
}

export function isJudge(user: User) {
  return user.is_jury_member;
}

export function getUserType(user: User): UserType {
  if (isSuperAdmin(user)) {
    return 'admin_super';
  }

  if (isAdmin(user)) {
    return 'admin_basic';
  }

  if (isJudge(user)) {
    return 'judge';
  }

  return 'applicant';
}
