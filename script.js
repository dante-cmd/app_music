const fs = require('node:fs');
var shell = require('shelljs');

// ----------------------------------------------------------------

const path_folder_songs = "C:/Users/dante/app_music/input songs"
const path_folder_out = "C:/Users/dante/app_music/output songs"
const path_file_effect_song = "C:/Users/dante/app_music/effect/dog-barking-70772.mp3"
const path_file_img = "C:/Users/dante/app_music/mario_bros.jpg"

const first_time_apply = "00:10"
const second_time_apply = "00:50"

const path_folder_normalize = `${__dirname}/normalized songs`
const name_cd  = "mix_1"

// ----------------------------------------------------------------
const input_name_dir = path_folder_songs.split("/").slice('-1')[0]
const walk_root = path_file_effect_song.split("/").slice('-2')
const effect_dir = walk_root[0]
const effect_file_name = walk_root[1]

// ----------------------------------------------------------------
shell.config.execPath = 'C:/Program Files/nodejs/node.exe'


// Get items {name, path} from path folder
const getItems = (pathFolder) => {
    try {
        const files = fs.readdirSync(pathFolder, {withFileTypes: true})
        const data = files.map((item) => {
            return {songPath:`${pathFolder}/${item.name}`}
        })
        return data
        
    } catch (error) {
        return false
    }
}



const convertMilliseconds = (x) => {

    const hourList = x.split(':')
    const minutes = hourList[0]
    const seconds = hourList[1]
    return (Number(minutes)*60 + Number(seconds))*1000
}

const normalAudio = (pathFileInput, pathFileOut) => {
    // `ffmpeg -i  "${pathFileInput}" -af loudnorm=I=-16:LRA=11:TP=-1.5 "${pathFileOut}"`
    const passToffmpeg = `ffmpeg -y -i  "${pathFileInput}" -af loudnorm=I=-16:TP=-1.5:LRA=11 "${pathFileOut}"`
    return passToffmpeg}


const getQuery = (songPath, effectAudioPath, first_time_apply, second_time_apply, imgPath, outSongPath) => {
            
    let firstMix = convertMilliseconds(first_time_apply)
    firstMix = firstMix.toString()
    let secondMix = convertMilliseconds(second_time_apply)
    secondMix = secondMix.toString()

    const passToffmpeg = `ffmpeg -y \
  -i "${songPath}" \
  -i "${effectAudioPath}" \
  -i "${effectAudioPath}" \
  -i "${imgPath}" \
  -filter_complex "[1:a]adelay=${firstMix}|${firstMix}[a1];\
                   [2:a]adelay=${secondMix}|${secondMix}[a2];\
                   [0:a][a1][a2]amix=inputs=3:duration=first:dropout_transition=2,volume=2.0[aout];\
                   [aout]loudnorm=I=-16:LRA=11:TP=-1.5" \
  -map 3:0 \
  -id3v2_version 3 \
  -metadata:s:v title="Album cover" \
  -metadata:s:v comment="Cover (front)" \
  -ar 44100 \
  -ac 2 \
  -b:a 320k \
  "${outSongPath}"`;
    //const passToffmpeg = `ffmpeg -y -i "${songPath}" -i "${effectAudioPath}" -i "${effectAudioPath}" -i "${imgPath}" -filter_complex "[1:a]volume=0.5,adelay=${firstMix}|${firstMix}[a1];[2:a]volume=1.0,adelay=${secondMix}|${secondMix}[a2];[0:a][a1][a2]amix=inputs=3:duration=longest:dropout_transition=0" -map 3:0 -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" -ar 44100 -ac 2 -b:a 320k "${outSongPath}"`
    //const passToffmpeg = `ffmpeg -y -i "${songPath}" -i "${effectAudioPath}" -filter_complex  "[0:0]volume=1.8[a];[1:0]volume=0.9[b];[a][b]amix=inputs=2:duration=longest" -c:a libmp3lame "${outSongPath}"`
    return passToffmpeg
}

const execute = (query) => {
    const resp = shell.exec(query);
    //shell.exec(`Test-Path "${outSongPath}"`)

    if (resp.code !== 0) {
        shell.exit(1);
    } else {
        shell.echo("Run passToffmpeg file");
    }
}




// 1. If exists normalized songs folder remove it

if (fs.existsSync(path_folder_normalize)) {
    fs.rmSync(path_folder_normalize, { recursive: true , force: true});
    console.log('Folder deleted!');
}


fs.mkdir(path_folder_normalize, (err) => {
    if (err) throw err;
    console.log('Folder created!'); 
})



// 2. create new folder normalized songs
fs.mkdir(`${path_folder_normalize}/${input_name_dir}`, (err) => {
    if (err) throw err;
    console.log('Folder created!'); 
})

fs.mkdir(`${path_folder_normalize}/${effect_dir}`, (err) => {
    if (err) throw err;
    console.log('Folder created!'); 
})



// // `${path_folder_normalize}/${input_name_dir}/${effect_dir}`
// //`${path_folder_normalize}/${input_name_dir}`

// // console.log(input_name_dir, effect_dir, effect_file_name)
// 3. normalize songs using ffmpeg

const items = getItems(path_folder_songs)

items.forEach((element) => {
    const {songPath} = element
    const [name_dir, name_file]=songPath.split('/').slice('-2')
    element["songPathNormal"] = `${path_folder_normalize}/${name_dir}/${name_file}`
    
})

const path_file_effect_song_normal = `${path_folder_normalize}/${effect_dir}/${effect_file_name}`

execute(normalAudio(path_file_effect_song, path_file_effect_song_normal))

items.forEach(element => {
    const {songPath, songPathNormal} = element
    execute(normalAudio(songPath, songPathNormal))
})

items.forEach(element => {
    const {songPath, songPathNormal} = element
    const name_file=songPathNormal.split('/').slice('-1')[0]
    const outSongPath = `${path_folder_out}/${name_file}`
    execute(getQuery(songPathNormal, path_file_effect_song_normal, 
        first_time_apply, second_time_apply, path_file_img, outSongPath)    )
})

// // getQuery(songPathNormal, path_file_effect_song, first_time_apply, second_time_apply, path_file_img, outSongPath)
// // execute(getQuery(songPath, path_file_effect_song, first_time_apply, second_time_apply, path_file_img, outSongPath))
// // console.log(outSongPath)