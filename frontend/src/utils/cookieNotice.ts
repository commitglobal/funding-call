import cookie from 'js-cookie';

export const getShowCookieNotice = () => {
  const ts = cookie.get('ts');

  return ts !== 'true' && ts !== 'false';
};

export const acceptCookieNotice = () => {
  cookie.set('ts', 'true', { expires: 365 });
};

export const rejectCookieNotice = () => {
  cookie.set('ts', 'false', { expires: 1 });
};
