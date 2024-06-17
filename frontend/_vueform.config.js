import fr_CA from '@vueform/vueform/locales/fr_CA'
import vueform from '@vueform/vueform/dist/vueform'
import { defineConfig } from '@vueform/vueform'

import '@vueform/vueform/dist/vueform.css';

export default defineConfig({
  theme: vueform,
  locales: { fr_CA },
  locale: 'fr_CA',
})