import { InternalLink } from '@/components/InternalLink';
import { LoginForm } from '@/components/LoginForm';
import { UsersFormContainer } from '@/components/UsersFormContainer';
import { applicantsUrls } from '@/constants/urlsConfig';
import LayoutDefault from '@/layouts/LayoutDefault';
import { useNotifyActions } from '@/stores/useNotifyStore';
import { CommonProps } from '@/types/CommonProps';
import { usePage } from '@inertiajs/react';

export default function Index() {
  const {
    props: { flash_messages },
  } = usePage<CommonProps>();

  const { notify } = useNotifyActions();
  if (flash_messages && flash_messages.length > 0) {
    notify(flash_messages, flash_messages[0].level_tag);
  }

  return (
    <div className='flex h-full max-w-3xl'>
      <UsersFormContainer
        subTitle={
          <>
            <div className='text-sm text-gray-600'>Nu ai cont?</div>
            <InternalLink
              color='text-purple-600'
              fontSize='text-sm'
              name='Înregistrează-te acum'
              to={applicantsUrls.register}
              underline={false}
            />
          </>
        }
        title='Autentifică-te în cont'
      >
        <LoginForm />
      </UsersFormContainer>
    </div>
  );
}

Index.layout = LayoutDefault;
