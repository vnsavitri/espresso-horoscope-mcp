module.exports = {
  multipass: true,
  js2svg: { pretty: true, indent: 2 },
  plugins: [
    'removeDoctype',
    'removeXMLProcInst',
    'removeComments',
    'removeMetadata',
    'removeEditorsNSData',
    'cleanupAttrs',
    'convertStyleToAttrs',
    'cleanupNumericValues',
    'convertPathData',
    'convertTransform',
    'removeUnknownsAndDefaults',
    'removeUselessStrokeAndFill',
    { name: 'removeViewBox', active: false }
  ],
};
