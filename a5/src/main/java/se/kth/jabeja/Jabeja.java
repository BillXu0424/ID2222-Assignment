package se.kth.jabeja;

import org.apache.log4j.Logger;
import se.kth.jabeja.config.AnnealingPolicy;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.NodeSelectionPolicy;
import se.kth.jabeja.io.FileIO;
import se.kth.jabeja.rand.RandNoGenerator;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Jabeja {
    final static Logger logger = Logger.getLogger(Jabeja.class);
    private final Config config;
    private final HashMap<Integer/*id*/, Node/*neighbors*/> entireGraph;
    private final List<Integer> nodeIds;
    private int numberOfSwaps;
    private int round;
    private float T;
    private boolean resultFileCreated = false;

    //-------------------------------------------------------------------
    public Jabeja(HashMap<Integer, Node> graph, Config config) {
        this.entireGraph = graph;
        this.nodeIds = new ArrayList(entireGraph.keySet());
        this.round = 0;
        this.numberOfSwaps = 0;
        this.config = config;
        this.T = config.getTemperature();
    }


    //-------------------------------------------------------------------
    public void startJabeja() throws IOException {
        for (round = 0; round < config.getRounds(); round++) {
            for (int id : entireGraph.keySet()) {
                sampleAndSwap(id);
            }

            //one cycle for all nodes have completed.
            //reduce the temperature
            saCoolDown();
            report();
        }
    }

    /**
     * Simulated analealing cooling function
     */
    private void saCoolDown() {
        // TODO for second task
        if (config.getAnnealingPolicy() == AnnealingPolicy.DEFAULT) {
            if (T > 1)
                T -= config.getDelta();
            if (T < 1)
                T = 1;
        } else {
            if (T > config.getMinTemperature()) {
                T *= config.getDecay();
            }
            if (T < config.getMinTemperature()) {
                T = config.getMinTemperature();
            }
        }
    }

    /**
     * Sample and swap algorith at node p
     *
     * @param nodeId
     */
    private void sampleAndSwap(int nodeId) {
        Node nodep = entireGraph.get(nodeId);
        Node partner = null;

        if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
                || config.getNodeSelectionPolicy() == NodeSelectionPolicy.LOCAL) {
            // swap with random neighbors
            // TODO
            Integer[] neighbors = getNeighbors(nodep);
            partner = findPartner(nodeId, neighbors);
        }

        if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
                || config.getNodeSelectionPolicy() == NodeSelectionPolicy.RANDOM) {
            // if local policy fails then randomly sample the entire graph
            // TODO
            if (partner == null) {
                Integer[] samples = getSample(nodeId);
                partner = findPartner(nodeId, samples);
            }
        }

        // swap the colors
        // TODO
        if (partner != null) {
            int qColor = partner.getColor();
            partner.setColor(nodep.getColor());
            nodep.setColor(qColor);
            numberOfSwaps++;
        }
    }

    public Node findPartner(int nodeId, Integer[] nodes) {
        Node nodep = entireGraph.get(nodeId);
        Node bestPartner = null;
        float alpha = config.getAlpha();
        double highestBenefit = 0;
        float dpcp = getDegree(nodep, nodep.getColor());

        for (Integer partnerId : nodes) {
            Node partner = entireGraph.get(partnerId);
            float dqcq = getDegree(partner, partner.getColor());
            float dpcq = getDegree(nodep, partner.getColor());
            float dqcp = getDegree(partner, nodep.getColor());
            double left = Math.pow(dpcp, alpha) + Math.pow(dqcq, alpha);
            double right = Math.pow(dpcq, alpha) + Math.pow(dqcp, alpha);

            if (config.getAnnealingPolicy() == AnnealingPolicy.DEFAULT) {
                double benefit = right * T - left;
                if (benefit > 0) {
                    if (benefit > highestBenefit) {
                        bestPartner = partner;
                        highestBenefit = benefit;
                    }
                }
            } else if (config.getAnnealingPolicy() == AnnealingPolicy.EXPONENTIAL) {
                double benefit = right - left;
                double ap = accProb(highestBenefit, benefit);
                if (ap < RandNoGenerator.nextDouble()) {
                    bestPartner = partner;
                    highestBenefit = benefit;
                }
            } else if (config.getAnnealingPolicy() == AnnealingPolicy.IMPROV_EXPONENTIAL) {
                double benefit = right - left;
                double ap = accProbImprov(highestBenefit, benefit);
                if (ap < RandNoGenerator.nextDouble()) {
                    bestPartner = partner;
                    highestBenefit = benefit;
                }
            }
        }

        // TODO

        return bestPartner;
    }

    private double accProb(double oldBenefit, double newBenefit) {
//        return Math.exp((oldBenefit - newBenefit) / T);
        return Math.log(1 + Math.exp((oldBenefit - newBenefit) / T));
    }

    private double accProbImprov(double oldBenefit, double newBenefit) {
        double benefitChange = (oldBenefit - newBenefit) / T;
        return Math.log(1 + Math.exp(benefitChange));
    }

    /**
     * The the degreee on the node based on color
     *
     * @param node
     * @param colorId
     * @return how many neighbors of the node have color == colorId
     */
    private int getDegree(Node node, int colorId) {
        int degree = 0;
        for (int neighborId : node.getNeighbours()) {
            Node neighbor = entireGraph.get(neighborId);
            if (neighbor.getColor() == colorId) {
                degree++;
            }
        }
        return degree;
    }

    /**
     * Returns a uniformly random sample of the graph
     *
     * @param currentNodeId
     * @return Returns a uniformly random sample of the graph
     */
    private Integer[] getSample(int currentNodeId) {
        int count = config.getUniformRandomSampleSize();
        int rndId;
        int size = entireGraph.size();
        ArrayList<Integer> rndIds = new ArrayList<Integer>();

        while (true) {
            rndId = nodeIds.get(RandNoGenerator.nextInt(size));
            if (rndId != currentNodeId && !rndIds.contains(rndId)) {
                rndIds.add(rndId);
                count--;
            }

            if (count == 0)
                break;
        }

        Integer[] ids = new Integer[rndIds.size()];
        return rndIds.toArray(ids);
    }

    /**
     * Get random neighbors. The number of random neighbors is controlled using
     * -closeByNeighbors command line argument which can be obtained from the config
     * using {@link Config#getRandomNeighborSampleSize()}
     *
     * @param node
     * @return
     */
    private Integer[] getNeighbors(Node node) {
        ArrayList<Integer> list = node.getNeighbours();
        int count = config.getRandomNeighborSampleSize();
        int rndId;
        int index;
        int size = list.size();
        ArrayList<Integer> rndIds = new ArrayList<Integer>();

        if (size <= count)
            rndIds.addAll(list);
        else {
            while (true) {
                index = RandNoGenerator.nextInt(size);
                rndId = list.get(index);
                if (!rndIds.contains(rndId)) {
                    rndIds.add(rndId);
                    count--;
                }

                if (count == 0)
                    break;
            }
        }

        Integer[] arr = new Integer[rndIds.size()];
        return rndIds.toArray(arr);
    }


    /**
     * Generate a report which is stored in a file in the output dir.
     *
     * @throws IOException
     */
    private void report() throws IOException {
        int grayLinks = 0;
        int migrations = 0; // number of nodes that have changed the initial color
        int size = entireGraph.size();

        for (int i : entireGraph.keySet()) {
            Node node = entireGraph.get(i);
            int nodeColor = node.getColor();
            ArrayList<Integer> nodeNeighbours = node.getNeighbours();

            if (nodeColor != node.getInitColor()) {
                migrations++;
            }

            if (nodeNeighbours != null) {
                for (int n : nodeNeighbours) {
                    Node p = entireGraph.get(n);
                    int pColor = p.getColor();

                    if (nodeColor != pColor)
                        grayLinks++;
                }
            }
        }

        int edgeCut = grayLinks / 2;

        logger.info("round: " + round +
                ", edge cut:" + edgeCut +
                ", swaps: " + numberOfSwaps +
                ", migrations: " + migrations);

        saveToFile(edgeCut, migrations);
    }

    private void saveToFile(int edgeCuts, int migrations) throws IOException {
        String delimiter = "\t\t";
        String outputFilePath;

        //output file name
        File inputFile = new File(config.getGraphFilePath());
        if (config.getAnnealingPolicy() == AnnealingPolicy.DEFAULT) {
            outputFilePath = config.getOutputDir() +
                    File.separator +
                    inputFile.getName() + "_" +
                    "NS" + "_" + config.getNodeSelectionPolicy() + "_" +
                    "GICP" + "_" + config.getGraphInitialColorPolicy() + "_" +
                    "AP" + "_" + config.getAnnealingPolicy() + "_" +
                    "T" + "_" + config.getTemperature() + "_" +
                    "D" + "_" + config.getDelta() + "_" +
                    "RNSS" + "_" + config.getRandomNeighborSampleSize() + "_" +
                    "URSS" + "_" + config.getUniformRandomSampleSize() + "_" +
                    "A" + "_" + config.getAlpha() + "_" +
                    "R" + "_" + config.getRounds() + ".txt";
        } else {
            outputFilePath = config.getOutputDir() +
                    File.separator +
                    inputFile.getName() + "_" +
                    "NS" + "_" + config.getNodeSelectionPolicy() + "_" +
                    "GICP" + "_" + config.getGraphInitialColorPolicy() + "_" +
                    "AP" + "_" + config.getAnnealingPolicy() + "_" +
                    "T" + "_" + config.getTemperature() + "_" +
                    "MT" + "_" + config.getMinTemperature() + "_" +
                    "D" + "_" + config.getDecay() + "_" +
                    "RNSS" + "_" + config.getRandomNeighborSampleSize() + "_" +
                    "URSS" + "_" + config.getUniformRandomSampleSize() + "_" +
                    "A" + "_" + config.getAlpha() + "_" +
                    "R" + "_" + config.getRounds() + ".txt";
        }

        if (!resultFileCreated) {
            File outputDir = new File(config.getOutputDir());
            if (!outputDir.exists()) {
                if (!outputDir.mkdir()) {
                    throw new IOException("Unable to create the output directory");
                }
            }
            // create folder and result file with header
            String header = "# Migration is number of nodes that have changed color.";
            header += "\n\nRound" + delimiter + "Edge-Cut" + delimiter + "Swaps" + delimiter + "Migrations" + delimiter + "Skipped" + "\n";
            FileIO.write(header, outputFilePath);
            resultFileCreated = true;
        }

        FileIO.append(round + delimiter + (edgeCuts) + delimiter + numberOfSwaps + delimiter + migrations + "\n", outputFilePath);
    }
}
