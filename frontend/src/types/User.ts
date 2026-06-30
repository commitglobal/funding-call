import { array, boolean, Infer, nullable, number, object, optional, string } from 'superstruct';

export type User = Infer<typeof User>;

export const User = object({
  agree_terms: optional(boolean()),
  avatar: optional(string()),
  email: string(),
  first_name: string(),
  id: number(),
  v1_id: optional(number()),
  is_active: boolean(),
  is_superadmin_member: optional(boolean()),
  is_admin_member: optional(boolean()),
  is_applicant_member: optional(boolean()),
  is_jury_member: optional(boolean()),
  is_staff_member: optional(boolean()),
  is_active_judge: optional(boolean()),
  is_superuser: optional(boolean()),
  is_staff: optional(boolean()),
  last_name: string(),
  last_login: optional(string()),
  last_edit: optional(string()),
  date_joined: optional(string()),
  role: optional(string()),
  agree_newsletter: optional(boolean()),
  groups: optional(array()),
  user_permissions: optional(array()),
  profile__agree_newsletter: optional(nullable(boolean())),
});

export type UserType = 'applicant' | 'admin_basic' | 'admin_super' | 'judge';


export const applicantsConst = 'applicants';
export const staffConst = 'staff';

export type UserRouteType = typeof applicantsConst | typeof staffConst;
