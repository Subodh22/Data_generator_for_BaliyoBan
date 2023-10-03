import {PrismaClient} from '@prisma/client'
const fs = require('fs')
const prisma = new PrismaClient()
 
const influencer_name = "Strength Training Program"
let dayCounter:number = 1
let planCounter:number = 0
async function Uploader(){
    const workout_celeb =await prisma.workoutCeleb.create({
        data:{
            name:influencer_name,
            ratings:"2",
            planType:"plan"
                
        }
       })

    const weekStructure =  fs.readFileSync('../Json_table/'+influencer_name+'/Week_Structure.json','utf8')
    const Week_data=JSON.parse(weekStructure);

    for (const weekD of Week_data.WeekStructure.Struc)
    {
        planCounter+=1
        let NameWeek = (weekD.name.split("."))[0]
         console.log(NameWeek)
         console.log(weekD)
    


   const structure =fs.readFileSync('../Json_table/'+influencer_name+"/"+NameWeek+'/Structure.json','utf8')
   const structure_data=JSON.parse(structure);
    
    
  
   const Cplan = await prisma.plan.create({
    data:{
        planName:NameWeek,
        workoutId:workout_celeb.id,
        currentStatus:"Loading",
        currentWeek:"Week 1",
        order:planCounter
        
        
         
        
    }
})
   
   
   let routineOrder:number=0
   for (const routineData of structure_data.workout_celeb.Routine){
   
    const nameofD:string[]=Object.values(routineData) 
    let weekNames:string  
    weekNames=nameofD[0]
    // structure_for_week.push(nameofD[0])

    const routine = await prisma.routine.create({
        data:{
            weekRoutine:"Day"+dayCounter,
            workoutCeleb:{connect:{id:workout_celeb.id}},
            order:routineOrder,
            planId:Cplan.id
        }

    })
    dayCounter+=1
    
   
    const sequence = fs.readFileSync('../Json_table/'+influencer_name+'/'+NameWeek+'/'+weekNames+'.json','utf8')
    const sequence_data = JSON.parse(sequence)
    let exerciseOrder :number=0
    for (const exe of sequence_data["Sequence_init"]["Exercises"]){
         
        const exercise = await prisma.exercise.create({
                data:{
                        name:exe["Name"],
                        type:exe["Type"],
                        setType:exe["Set Type"],
                        videoId:exe["videoId"],
                        machineSettings:exe["MachineSettings"],
                        routine: {connect: {id:routine.id}},
                        order:exerciseOrder
        
        
                    }

                })

        let setOrder:number=0
        for (const seter of exe["Sets"]){
            const set = await prisma.set.create({
                data:{
                    name:seter["Name"],
                    type:seter["Type"],
                    restTime:seter["Rest Time"],
                    volume:seter["Volume"],
                    weight:seter["Weight"],
                    exercise :{connect:{id:exercise.id}},
                    order:setOrder,
                    routineId: routine.id
                }
            })
            setOrder++
            console.log(setOrder)
                }
                setOrder=0
                
        exerciseOrder++
            }
    exerciseOrder=0
    
    routineOrder++
   }
 
    
}
}

async function deleteAll(){
    await prisma.set.deleteMany()
    await prisma.exercise.deleteMany()
    await prisma.routine.deleteMany()
    await prisma.userToWork.deleteMany()
    await prisma.personalSets.deleteMany()
    await prisma.userSetHistory.deleteMany()
    await prisma.sessions.deleteMany()
    await prisma.personalExercise.deleteMany()
    await prisma.userDetails.deleteMany()
    await prisma.testers.deleteMany()
    await prisma.plan.deleteMany()
    await prisma.personalPlan.deleteMany()
   

    const getter=await prisma.workoutCeleb.deleteMany()
    console.log("dd")
    console.log(getter)
}

async function getWorkout(){
    let celeb:string=influencer_name
   const get= await prisma.workoutCeleb.findMany({
    where:{
        name: celeb
    }
   })
    
   const workout = await prisma.exercise.findMany( )
   if (workout !== null   ){
    for(const i of workout){
        console.log(i["name"] )
    }

   }
   console.log(get)
}
console.log("ddss")


Uploader().
    then(async()=>
    {
        await prisma.$disconnect()
    }).catch(async(e)=>{
        console.error(e)
        await prisma.$disconnect()
        process.exit(1)
    })