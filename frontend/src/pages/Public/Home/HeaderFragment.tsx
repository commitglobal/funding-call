import { authUrls } from '@/constants/urlsConfig';
import { LinkButton } from '@components/LinkButton';


export function HeaderFragment() {
  return (
    <div>
      <h2 className='font-amalia-bold text-4xl lg:text-6xl text-black mb-5'>
        Hello
      </h2>
      <div className='flex flex-col gap-y-6 flex-1'>
        <div className='flex flex-row gap-6'>
          <LinkButton to='/about/' variant='outlined'>
            Află mai multe
          </LinkButton>
          <LinkButton to={authUrls.login} variant='contained'>
            Login
          </LinkButton>
        </div>
      </div>
    </div>
  );
}
