import { applicantsUrls } from '@/constants/urlsConfig';
import { LinkButton } from '@components/LinkButton';
import { usePage } from '@inertiajs/react';
import { HomePageProps } from './HomePageProps';

export function HeaderFragment() {
  const {
    props: {},
  } = usePage<HomePageProps>();

  return (
    <div>
      <h2 className='font-amalia-bold text-4xl lg:text-6xl text-black mb-5'>
        header
      </h2>
      <div className='flex flex-col gap-y-6 flex-1'>
        <div className='flex flex-row gap-6'>
          <LinkButton to='/about/' variant='outlined'>
            Află mai multe
          </LinkButton>
          <LinkButton to={applicantsUrls.register} variant='contained'>
            Înscrie-te în program
          </LinkButton>
        </div>
      </div>
    </div>
  );
}
