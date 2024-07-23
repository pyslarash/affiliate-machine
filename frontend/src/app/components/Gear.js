import { motion } from 'framer-motion';
import "../gears.css"
import { Cog8ToothIcon } from '@heroicons/react/24/outline';

const Gear = ({ theme, small }) => {
    const spinTransition = {
        repeat: Infinity,
        ease: "linear",
        duration: 10,
    };

    return (
        <div className="gear-wrapper">
            {/* First gear */}
            <motion.div
                className="first-gear"
                animate={{ rotate: 360 }}
                transition={spinTransition}
            >
                <Cog8ToothIcon />                
            </motion.div>

            {/* Second gear */}
            <motion.div
                className="second-gear"
                animate={{ rotate: -360 }}
                transition={spinTransition}
            >
                <Cog8ToothIcon />          
            </motion.div>
        </div>
    );
};

export default Gear;
