import webpack from 'webpack'

module.exports = {

  server: {
    host: 'localhost',
    port: 3001
  },
  head: {
    meta: [{
      charset: 'utf-8',
    }, {
      name: 'viewport',
      content: 'width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no',
    }],
    cookie: {}
  },
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/pwa',
  ],
  buildModules: [
    '@nuxtjs/vuetify',
    '@nuxtjs/moment',
  ],
  plugins: [
    {src: '~/plugins/axios.js', mode: 'client'}
  ],

  // pwa: {
  //     icon: {
  //         iconSrc: 'static/icon.png'
  //     },
  //     manifest: {
  //         name: 'node_express_study_final'
  //     },
  //     workbox: {
  //         dev: true,
  //         runtimeCaching: [{
  //             urlPattern: 'http://localhost:4001/.*',
  //             method: 'GET'
  //         }, {
  //             urlPattern: 'http://localhost:5001/.*',
  //             method: 'GET'
  //         }]
  //     },
  // }
};
