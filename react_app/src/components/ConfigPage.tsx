import React, {useState, useEffect} from 'react';
import {Slider, Button} from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import axios from 'axios';
import socketClientIO from 'socket.io-client';

interface Props {

}

interface Log {
    name: string,
    seated_time: number,
    arrive_time: number,
    visit_duration: number,
    patience: number,
}

const config = {
    patience: {
        min: 0,
        max: 120
    },
    duration: {
        min: 0,
        max: 120
    },
    revenue: {
        min: 0,
        max: 100,
    },
    capacity: {
        min: 0,
        max: 500
    }
}

export const ConfigPage: React.FC<Props> = () => {
    
    const [patience, setPatience] = useState<number>(10);
    const [duration, setDuration] = useState<number>(30);
    const [revenue, setRevenue] = useState<number[]>([5, 10, 15]);
    const [capacity, setCapacity] = useState<number>(40);
    const [logs, setLogs] = useState<Log[]>([]);

    useEffect(() => {
        const socket = socketClientIO();
        socket.on('sim-result', (data: any) => {
            console.log("result of simulation")
            console.log(data);
        })
    })

    useEffect(() => {
        const socket = socketClientIO();
        socket.on('sim-update', (data: Log) => {
            console.log(data)
            setLogs(logs => [...logs, data]);
        });
    }, [logs])


    const patienceMarks = [
        {value: config.patience.min, label: `${config.patience.min} minutes`},
        {value: config.patience.max, label: `${config.patience.max} minutes`},
    ]

    const durationMarks = [
        {value: config.duration.min, label: `${config.duration.min} minutes`},
        {value: config.duration.max, label: `${config.duration.max} minutes`},
    ]
    const revenueMarks = [
        {value: config.revenue.min, label: `$${config.revenue.min}`},
        {value: config.revenue.max, label: `$${config.revenue.max}`},
    ]
    const capacityMarks = [
        {value: config.capacity.min, label: `${config.capacity.min} seats`},
        {value: config.capacity.max, label: `${config.capacity.max} seats`},
    ]

    const startSimulation = () => {
        setLogs([])
        let data = {
            patience: patience,
            duration: duration,
            revenue: revenue,
            capcity: capacity
        }
        console.log("Simulation data: ", data);
        
        axios.post('/api/v1/simulate', data).then(res => {
            console.log("Data sent")
        }).catch(err => console.log(err));
    }

 

    return (
        <div>
            <h1>Config Page</h1>
            <Typography id="duration-slider" gutterBottom>
                Visit Duration
            </Typography>
            <Slider 
                name="duration"
                aria-labelledby="duration-slider"
                valueLabelDisplay="auto"
                value={duration}
                onChange={(event: object, value: any) => {setDuration(Number(value))}}
                step={5}
                marks={durationMarks}
                min={config.duration.min}
                max={config.duration.max}
            />
            <Typography id="patience-slider" gutterBottom >
                Patience
            </Typography>
            <Slider
                name="patience"
                aria-labelledby="patience-slider"
                valueLabelDisplay="auto"
                value={patience}
                onChange={(event: object, value: any) => setPatience(Number(value))}
                step={5}
                marks={patienceMarks}
                min={config.patience.min}
                max={config.patience.max}
            />
            <Typography id="revenue-slider">
                Revenue
            </Typography>
            <Slider
                name="revenue"
                aria-labelledby="revenue-slider"
                valueLabelDisplay="auto"
                value={revenue}
                onChange={(event: object, value: any) => {
                    setRevenue(value)
                    console.log(value)
                }} 
                marks={revenueMarks}
                step={5}
                min={config.revenue.min}
                max={config.revenue.max}
            />
            <Typography id="capacity-slider">
                Capacity
            </Typography>
            <Slider
                name="capacity"
                aria-labelledby="capacity-slider"
                valueLabelDisplay="auto"
                value={capacity}
                onChange={(event: object, value: any) => setCapacity(Number(value))}
                step={1}
                marks={capacityMarks}
                min={config.capacity.min}
                max={config.capacity.max}
            />
            <Button 
                color="primary"
                variant="contained"
                onClick={() => startSimulation()}
            >
                Start Simulation
            </Button>

            <div>
                {logs.map(log => {
                    if (log['visit_duration'] > 0) {
                        return (
                            <div>
                                Waited for {log['seated_time'] - log['arrive_time']} and stayed for {log['visit_duration']}.
                            </div>
                        )
                    }
                    else {
                        return (
                            <div>
                                Left after waiting {log['patience']}.
                            </div>
                        )
                    }
                })}
            </div>

        </div>
    )
}