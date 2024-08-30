import * as echarts from "./echarts.js"

export function ssr(width,height,option){
    let e = echarts.init(
        null,null,{
            renderer: 'svg',
            ssr:true,
            width:width,
            height:height
        }
    
    );
    option = JSON.parse(option)
    // option.animation = false;
    e.setOption(option);
    const svgStr = e.renderToSVGString();
    e.dispose();
    e = null;
    console.log(svgStr);
}

const args = process.argv.slice(2);
const width = parseInt(args[0]);
const height = parseInt(args[1]);
const options = process.argv.slice(4);
options.forEach(option => {
    ssr(width,height,option);
});
