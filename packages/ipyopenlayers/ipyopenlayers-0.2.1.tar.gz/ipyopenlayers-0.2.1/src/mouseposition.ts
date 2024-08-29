// Copyright (c) QuantStack
// Distributed under the terms of the Modified BSD License.
import { DOMWidgetModel, ISerializers } from '@jupyter-widgets/base';
import { BaseControlModel, BaseControlView } from './basecontrol';
import MousePosition from 'ol/control/MousePosition.js';

import 'ol/ol.css';
import { MODULE_NAME, MODULE_VERSION } from './version';
import '../css/widget.css';

export class MousePositionModel extends BaseControlModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: MousePositionModel.model_name,
      _model_module: MousePositionModel.model_module,
      _model_module_version: MousePositionModel.model_module_version,
      _view_name: MousePositionModel.view_name,
      _view_module: MousePositionModel.view_module,
      _view_module_version: MousePositionModel.view_module_version,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Ajoutez ici tous les sérialiseurs supplémentaires
  };

  static model_name = 'MousePositionModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'MousePositionView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}
export class MousePositionView extends BaseControlView {
  createObj() {
    this.obj = new MousePosition({
      className: 'ol-mouse-position',
    });
  }
}
