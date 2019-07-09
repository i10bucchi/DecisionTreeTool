# Decision Tree Tool

## Overview

このツールは決定木分析の実行と可視化を行うためのツールです.
現在は回帰決定木分析のみに対応しています.

## Requirement

### python3

- numpy
    ```
    $ pip install numpy
    ```

- pandas
    ```
    $ pip3 install pandas
    ```

- scikit-learn
    ```
    $ pip3 install scikit-learn
    ```

## Instllation

```
// クローンします
$ git clone https://github.com/i10bucchi/DecisionTreeTool.git
// dataという名前でディレクトリを作ってくだいさい
$ mkdir ./DecisionTreeTool/data
```

## Usage

### Snypet

```
$ python3 tree.py [-i] [-o] [-c] [--criterion] [--splitter] [--max_depth] [--min_samples_split] [--min_samples_leaf] [--min_weight_fraction_leaf] [--max_features] [--random_state] [--max_leaf_nodes] [--min_impurity_decrease] [--presort]
```

### Command


- [-h --help]
    コマンドオプションと使用例を表示します.

- [-i --input_csv]
    学習, テストデータとして使用するcsvファイルのパスを渡します. このオプションは必ず指定しなければなりません.

- [-o --objective_variable]
    目的変数を指定します. csvファイルのカラム名と同じものを指定する必要があります. このオプションは必ず指定しなければなりません.

- [-c --categolical_variable]
    ダミー変数化を行いたい変数を指定します. 指定されない場合は自動でダミー変数化されます. 詳しくはpandas.get_dummyの使用を確認ください. 複数の変数を指定する場合は","を使用して繋げてください. csvファイルのカラム名と同じものを指定する必要があります.

他, [ --option_name ]の形で[sklearn.tree.DecisionTreeRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html)のオプションを指定できます. 

### Example

以下のコマンドはtree.pyがあるディレクトリ内での実行を想定しています.

```
$ python3 tree.py -p ./data.csv -o 変数名2 -c 変数名2,変数名3 --max_depth=7 > result.html
```

### Data

csvファイルは1列目をインデックスとしてプログラムに読み込まれます. よって以下のように整形してください.

_data.csv_
| index | 変数名1 | 変数名2 | 変数名3 | ... |
|:--:|:--:|:--:|:--:|:--:|
| ... | ... | ... | ... | ... |

### View

決定木分析結果の見方を説明します. -pオプションを指定してhtmlファイルを作成した方はブラウザにてファイルを開いてください.

#### 決定木

![Tree](https://user-images.githubusercontent.com/22851828/60765533-c9c3ab00-a0d6-11e9-9e4a-d328f8508768.png)

- ノードの持つ条件はノード上部に表示されます.

- ノードの色はノードの持つデータの平均値を表します. 高いほど暗く, 低いほど明るくなるように設定されています. ヒートマップと同様の見方となります.

- 各ノードをクリックすることで, 対象のノードが持つデータのヒストグラムが確認可能です.

- 各ノードに対してマウスオーバーすることでノードの以下の情報が表示されます.
    - サンプル数(sample)
    - 左子ノードへの分割サンプル数(sample_l)
    - 右子ノードへの分割サンプル数(sample_r)
    - 平均値(mu)

- ノードをつなぐ線(リンク)は色によって以下の意味を持ちます.
    - 灰色: 未収束
    - 緑色: 収束(分割結果がルートノードの60%の分散を持つことが収束したと判断される基準になります)

#### 最優推定モデル

![ML](https://user-images.githubusercontent.com/22851828/60733939-46e10a00-9f89-11e9-938a-d48c28cb7370.png)

決定木の下部に表示される線グラフは収束し, 信頼性があると判断されたノードの最優推定モデルです.

- 赤の線グラフはルートノードに対しての最優推定モデルです.
- 青の線グラフは収束し, 信頼性があると判断されたノードの最優推定モデルです.
    - この時, 対象となった子ノードから派生するノードに対しては, 信頼性があろうとも最優推定モデルは表示されません.
    - 収束の判断基準は, 対象ノードの分散が親ノードの分散の60%以下であることです.
    - 信頼性の判定基準は, 対象ノードのサンプル数が親ノードのサンプル数の10%以上であることです.
- 各線をマウスオーバーすることで対象のノード情報を表示することができます.