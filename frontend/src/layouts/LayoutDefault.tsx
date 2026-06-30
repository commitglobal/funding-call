import { Page } from '@inertiajs/core';
import { ReactNode } from 'react';
import { Notification } from '@/components/Notification';
import { CommonProps } from '@/types/CommonProps';
import { SimplifiedNavbar } from '@components/SimplifiedNavbar.tsx';
import { OldCookieBanner } from '@components/cookies/OldCookieBanner.tsx';


export default function LayoutDefault(page: Page<CommonProps>) {
  const deactivate_nav_banner = page.props.deactivate_nav_banner;
  const deactivate_cookie_banners = page.props.deactivate_cookie_banners;
  const activate_new_cookie_banners = page.props.activate_new_cookie_banners;
  const is_authenticated = page.props.is_authenticated || false;
  const user = page.props.user || null;

  const homepage_url = page.props.homepage_url || '/';
  const cookie_policy_url = page.props.cookie_policy_url;

  return (
    <div className='flex flex-col h-full'>
      {!deactivate_nav_banner &&
        <SimplifiedNavbar
          is_authenticated={is_authenticated}
          user={user}
          homepage_url={homepage_url} />
      }
      <main className='grow mt-20 text-black'>
        {page as unknown as ReactNode}
        <Notification />
      </main>

      {!deactivate_cookie_banners &&
        (activate_new_cookie_banners
            ? <>
            </>
            : <OldCookieBanner cookie_url={cookie_policy_url} />
        )
      }
    </div>
  );
}
