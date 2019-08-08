#ifndef Physics_Analysis_DDecayAlg_H
#define Physics_Analysis_DDecayAlg_H 

#include "GaudiKernel/AlgFactory.h"
#include "GaudiKernel/Algorithm.h"

class DDecayAlg : public Algorithm {

    public:
        DDecayAlg(const std::string& name, ISvcLocator* pSvcLocator);
        StatusCode initialize();
        StatusCode execute();
        StatusCode finalize();  

    private:

};
#endif
