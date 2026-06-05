import { BannerFragment } from './BannerFragment';
import { DetailsFragment } from './DetailsFragment';
import { HeaderFragment } from './HeaderFragment';
import LayoutDefault from '@/layouts/LayoutDefault';
import { RaiffeisenLogoSvg } from '@/components/RaiffeisenLogoSvg';
import { UELogoSvg } from '@/components/UELogoSvg';
import { images } from '@/constants/images';
import { CallToActionFragment } from './CallToActionFragment';
import { EligibilityFragment } from './EligibilityFragment';
import { HomePageProps } from './HomePageProps';
import { getCMSData } from '@/utils/getCMSData';
import { CMSImage } from '@/components/cms/CMSImage';

const defaultCms = {
  home_banner: {
    raw_content: `<img alt='' src='${images.home.homeBanner}' />`,
  },
  // home_first_logo: {
  //   raw_content: '',
  // },
  home_second_logo: {
    raw_content: `<img alt='' src='${images.general.euFundLogo}' />`,
  },
  // home_third_logo: {
  //   raw_content: '',
  // },
};

export default function Index({ cms }: HomePageProps) {
  const homeBanner = getCMSData('home_banner', defaultCms, cms);
  // const homeFirstLogo = getCMSData('home_first_logo', defaultCms, cms);
  const homeSecondLogo = getCMSData('home_second_logo', defaultCms, cms);
  // const homeThirdLogo = getCMSData('home_third_logo', defaultCms, cms);

  return (
    <>
      <div className='flex flex-col gap-y-24 max-w-7xl mx-auto pt-12 lg:pt-32 px-4'>
        <div className='absolute flex items-center left-0 right-0 top-30 lg:top-20 justify-center -z-1'>
          <CMSImage cms={homeBanner} />
        </div>
        <HeaderFragment />

        <div className='flex flex-col md:flex-row items-center justify-evenly gap-6'>
          {/* {homeFirstLogo.raw_content ? (
            <CMSImage cms={homeFirstLogo} />
          ) : ( */}
          <RaiffeisenLogoSvg />
          {/* )} */}
          <CMSImage cms={homeSecondLogo} />
          {/* {homeThirdLogo.raw_content ? (
            <CMSImage cms={homeThirdLogo} />
          ) : ( */}
          <UELogoSvg />
          {/* )} */}
        </div>

        <DetailsFragment />
      </div>

      <div className='py-20' />

      <EligibilityFragment />

      <CallToActionFragment />

      <BannerFragment />

    </>
  );
}

Index.layout = LayoutDefault;
