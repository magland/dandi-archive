import Vue from 'vue';
import Vuex from 'vuex';

import girder from '@/store/girder';
import myDandisets from '@/store/myDandisets';
import stats from '@/store/stats';

Vue.use(Vuex);


export default new Vuex.Store({
  modules: {
    girder,
    publicDandisets: myDandisets,
    myDandisets,
    stats,
  },
});
