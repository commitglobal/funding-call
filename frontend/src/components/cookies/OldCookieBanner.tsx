import { acceptCookieNotice, getShowCookieNotice, rejectCookieNotice } from '@/utils/cookieNotice.ts';
import { ExternalLink } from '@components/ExternalLink.tsx';
import { Button } from '@components/Button.tsx';
import { useState } from 'react';

type OldCookieBannerProps = {
  cookie_url: string;
};

export const OldCookieBanner = ({ cookie_url }: OldCookieBannerProps ) => {
  const [showCookieNotice, setShowCookieNotice] = useState(
    getShowCookieNotice(),
  );

  return (
    showCookieNotice && (
      <div className='fixed bottom-0 bg-white left-0 right-0 py-6 px-4 border-t z-10'>
        <div className='max-w-7xl m-auto grid gap-4 lg:grid-cols-12'>
          <div className='col-span-12 lg:col-span-10'>
            <div className='text-lg font-amalia-medium mb-2'>
              Utilizarea modulelor cookie
            </div>
            <div>
              Pentru a afla mai multe, citiți{' '}
              <ExternalLink
                color='text-purple-600'
                name='Politica de utilizare cookies'
                to={cookie_url}
              />
              .
            </div>
          </div>
          <div className='flex flex-col gap-3 col-span-12 lg:col-span-2 items-center justify-center'>
            <Button
              fullWidth
              variant='outlined'
              onClick={() => {
                rejectCookieNotice();
                setShowCookieNotice(false);
              }}
            >
              Refuz
            </Button>
            <Button
              fullWidth
              onClick={() => {
                acceptCookieNotice();
                setShowCookieNotice(false);
              }}
            >
              Sunt de acord
            </Button>
          </div>
        </div>
      </div>
    )
  );
};
