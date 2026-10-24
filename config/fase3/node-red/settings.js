const path = require('path');
const monitor = require('../../../src/fase3/node-red/monitor');
module.exports = {
  uiHost: '127.0.0.1',
  uiPort: Number(process.env.CARDIOIA_PORT || 1880),
  httpAdminRoot: '/editor',
  flowFile: path.join(process.env.CARDIOIA_RUNTIME_DIR || path.join(__dirname,'../../../.tools/runtime/fase3/node-red'),'flows.json'),
  functionGlobalContext: {
    cardioia: monitor,
    cardioiaConfig: {
      root: process.env.CARDIOIA_TOPIC_ROOT || monitor.ROOT,
      device: process.env.CARDIOIA_DEVICE_ID || monitor.DEVICE
    }
  },
  contextStorage: {default: {module: 'memory'}},
  editorTheme: {projects: {enabled: false}},
  logging: {console: {level: 'info', metrics: false, audit: false}}
};
