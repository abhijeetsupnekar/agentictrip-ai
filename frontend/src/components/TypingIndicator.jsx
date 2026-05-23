import { motion } from "framer-motion";

const TypingIndicator = () => {

    return (

        <div className="flex justify-start">

            <div className="bg-white/5 border border-white/10 rounded-3xl p-5 w-fit">

                <p className="text-sm text-gray-400 mb-3">
                    AgenticTrip AI is thinking...
                </p>

                <div className="flex gap-2">

                    {[0, 1, 2].map((dot) => (

                        <motion.div
                            key={dot}
                            animate={{
                                y: [0, -6, 0],
                            }}
                            transition={{
                                duration: 0.6,
                                repeat: Infinity,
                                delay: dot * 0.2,
                            }}
                            className="w-3 h-3 rounded-full bg-white"
                        />

                    ))}

                </div>

            </div>

        </div>

    );

};

export default TypingIndicator;