export async function onRequest({ request }) {
  const country=(request.headers.get('CF-IPCountry')||'').toUpperCase();
  const byCountry={CN:'zh-CN',HK:'zh-CN',MO:'zh-CN',TW:'zh-CN',IT:'it',SM:'it',VA:'it',US:'en',GB:'en',IE:'en',CA:'en',AU:'en',NZ:'en',ES:'es',MX:'es',AR:'es',FR:'fr',BE:'fr',DE:'de',AT:'de',CH:'de',JP:'ja',KR:'ko'};
  const lang=byCountry[country]||'en';
  return Response.redirect(new URL(`/${lang}/news/`,request.url),302);
}