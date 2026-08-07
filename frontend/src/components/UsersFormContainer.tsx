import { ReactNode } from 'react';
type UsersFormContainerProps = {
  children: ReactNode;
  subTitle?: ReactNode;
  title: string;
};

export function UsersFormContainer({
  children,
  subTitle,
  title,
}: UsersFormContainerProps) {
  return (
    <div className='basis-2/5 flex flex-col gap-y-8 grow px-4 lx:px-24 py-12'>
      <div>
        <div className='font-amalia-bold text-3xl'>{title}</div>
        <div className='flex gap-x-1'>
          {typeof subTitle === 'string' ? (
            <div className='text-sm text-gray-600'>{subTitle}</div>
          ) : (
            subTitle
          )}
        </div>
      </div>

      {children}
    </div>
  );
}
