export default function ({$axios, store}) {
  $axios.onRequest((config) => {
    console.log('axios cookie 요청', store.state.user.cookie);
    const cookie = store.state.user.cookie;
    if(cookie){
      config.headers.common['Authorization'] = `Token ${cookie}`;
    }
  })
}
