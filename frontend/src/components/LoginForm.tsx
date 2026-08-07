import { useForm, usePage } from '@inertiajs/react';
import { FormEventHandler, useCallback } from 'react';
import { apiPostUrls } from '@/constants/apiUrls';
import { handleChange } from '@/utils/handleChange';
import { Button } from './Button';
import { Checkbox } from './Checkbox';
import { InputField } from './InputField';
import { InternalLink } from './InternalLink';
import { UserRouteType } from '@/types/User';

type LoginFormData = {
  email: string;
  password: string;
  remember: boolean;
};

type LoginFormProps = {
  userRouteType?: UserRouteType;
};

export function LoginForm({ userRouteType = 'applicants' }: LoginFormProps) {
  const {
    props: { errors },
  } = usePage();
  const { data, setData, post, processing } = useForm<LoginFormData>({
    email: '',
    password: '',
    remember: false,
  });

  const handleSubmit = useCallback<FormEventHandler>(
    (e) => {
      e.preventDefault();
      post(apiPostUrls.usersLogin(), {
        preserveScroll: true,
      });
    },
    [post, userRouteType],
  );

  const formErrors = errors?.login;

  return (
    <>
      <form className='flex flex-col gap-y-6' onSubmit={handleSubmit} target="_blank">
        <InputField
          errors={formErrors?.email}
          label='Adresă de mail'
          name='email'
          onChange={handleChange<LoginFormData>('email', setData)}
          value={data.email}
        />

        <InputField
          errors={formErrors?.password}
          label='Parolă'
          name='password'
          onChange={handleChange<LoginFormData>('password', setData)}
          type='password'
          value={data.password}
        />

        <div className='flex justify-between'>
          <Checkbox
            checked={data.remember}
            label='Ține-mă minte'
            name='remember'
            onChange={(e) => setData('remember', e.target.checked)}
          />

          <InternalLink
            color='text-purple-600'
            fontSize='text-sm'
            name='Ți-ai uitat parola?'
            to={`/${userRouteType}/forgot-password/`}
            underline={false}
          />
        </div>
        <Button disabled={processing}>Autentifică-te în cont</Button>
      </form>
    </>
  );
}
