import { ForwardRefExoticComponent } from 'react';

export type SvgIcon =
  | ForwardRefExoticComponent<Omit<React.SVGProps<SVGSVGElement>, 'ref'>>
  | ((props: { className?: string }) => JSX.Element);
