import { HeaderFragment } from './HeaderFragment';
import LayoutDefault from '@/layouts/LayoutDefault';


export default function Index() {
  return (
    <>
      <div className='flex flex-col gap-y-24 max-w-7xl mx-auto pt-12 lg:pt-32 px-4'>
        <div className='absolute flex items-center left-0 right-0 top-30 lg:top-20 justify-center -z-1'>
          
        </div>
        <HeaderFragment />
      </div>

    </>
  );
}

Index.layout = LayoutDefault;
