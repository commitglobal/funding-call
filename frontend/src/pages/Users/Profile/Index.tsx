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
      Profile
    </div>
  );
}

Index.layout = LayoutDefault;
