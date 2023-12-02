package se.kth.jabeja.config;

public enum AnnealingPolicy {
    DEFAULT("DEFAULT"),
    EXPONENTIAL("EXPONENTIAL");

    String name;

    AnnealingPolicy(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return name;
    }
}
